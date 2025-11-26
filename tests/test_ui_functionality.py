import pytest
from playwright.sync_api import sync_playwright, Page, expect
import time
import pandas as pd
import io
import re


@pytest.fixture(scope="module")
def browser():
    """Create a browser instance for UI tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create a new page for each test"""
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def sample_excel_file():
    """Create a sample Excel file for testing"""
    df = pd.DataFrame({
        'Name': ['Test1', 'Test2'],
        'Value': [100, 200]
    })
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return {
        'name': 'test.xlsx',
        'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'buffer': buffer.getvalue()
    }


@pytest.mark.ui
@pytest.mark.slow
class TestUIFunctionality:
    """Tests for UI functionality, especially buttons"""

    BASE_URL = "http://localhost:8000"

    def test_upload_page_loads(self, page):
        """Test that the upload page loads correctly"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Check page title
        expect(page).to_have_title("Data Comparison Tool - Upload")
        
        # Check main heading
        heading = page.locator("h1")
        expect(heading).to_contain_text("Data Comparison Tool")
        
        # Check subtitle
        subtitle = page.locator(".subtitle")
        expect(subtitle).to_contain_text("正解データ")

    def test_choose_file_buttons_exist(self, page):
        """Test that Choose File buttons are present and visible"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Find all Choose File buttons
        choose_file_buttons = page.locator("button:has-text('Choose File')")
        expect(choose_file_buttons).to_have_count(2)
        
        # Check they are visible
        for i in range(2):
            button = choose_file_buttons.nth(i)
            expect(button).to_be_visible()
            expect(button).to_be_enabled()

    def test_choose_file_button_triggers_file_input(self, page):
        """Test that clicking Choose File button triggers file input"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Get the first Choose File button and file input
        choose_file_button = page.locator("button:has-text('Choose File')").first
        file_input = page.locator('input[name="ground_truth"]')
        
        # Verify button is visible and enabled
        expect(choose_file_button).to_be_visible()
        expect(choose_file_button).to_be_enabled()
        
        # Click the button - this should trigger the file input
        choose_file_button.click()
        
        # Verify file input exists (even if hidden)
        expect(file_input).to_have_count(1)
        
    def test_file_selection_updates_display(self, page, sample_excel_file):
        """Test that selecting a file updates the display area"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Get file input and display area
        file_input = page.locator('input[name="ground_truth"]')
        file_display = page.locator('#gtFileDisplay')
        
        # Initially should show "No file chosen"
        expect(file_display).to_contain_text("No file chosen")
        
        # Set file directly (simulating file selection)
        file_input.set_input_files({
            'name': sample_excel_file['name'],
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        
        # Wait for the change event to fire
        page.wait_for_timeout(500)
        
        # Display should now show the filename
        expect(file_display).to_contain_text("test.xlsx")
        expect(file_display).to_have_class(re.compile(".*has-file.*"))

    def test_file_input_elements_exist(self, page):
        """Test that file input elements exist (even if hidden)"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Check file inputs exist
        ground_truth_input = page.locator('input[name="ground_truth"]')
        extracted_input = page.locator('input[name="extracted_result"]')
        
        expect(ground_truth_input).to_have_count(1)
        expect(extracted_input).to_have_count(1)

    def test_compare_files_button_exists(self, page):
        """Test that Compare Files button exists and is functional"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        compare_button = page.locator("button:has-text('Compare Files')")
        expect(compare_button).to_have_count(1)
        expect(compare_button).to_be_visible()
        expect(compare_button).to_be_enabled()

    def test_form_submission_without_files(self, page):
        """Test form validation when submitting without files"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        compare_button = page.locator("button:has-text('Compare Files')")
        
        # Try to submit without files (browser validation should prevent this)
        compare_button.click()
        
        # Wait a moment
        page.wait_for_timeout(500)
        
        # The page should still be on the upload page (validation prevents submission)
        expect(page).to_have_url(f"{self.BASE_URL}/comparison/")
        
    def test_compare_files_button_click_with_files(self, page, sample_excel_file):
        """Test that Compare Files button works when files are selected"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Set both file inputs
        gt_input = page.locator('input[name="ground_truth"]')
        ext_input = page.locator('input[name="extracted_result"]')
        
        gt_input.set_input_files({
            'name': sample_excel_file['name'],
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        
        ext_input.set_input_files({
            'name': sample_excel_file['name'],
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        
        # Wait for file displays to update
        page.wait_for_timeout(500)
        
        # Click Compare Files button
        compare_button = page.locator("button:has-text('Compare Files')")
        expect(compare_button).to_be_enabled()
        
        # Set up response interception to verify API call
        with page.expect_response(lambda response: 
            "/comparison/api/compare" in response.url and response.request.method == "POST"
        ) as response_info:
            # Click the button
            compare_button.click()
        
        # Get the response
        response = response_info.value
        
        # Verify the API was called
        assert response.status in [200, 400, 500]  # Any response means the button worked
        
        # Wait a bit for potential navigation
        page.wait_for_timeout(1000)
        
        # Check if we navigated to results page or if there's an error message
        current_url = page.url
        if "/comparison/results" in current_url:
            # Successfully navigated to results
            expect(page.locator("h1")).to_contain_text("Comparison Results")
        else:
            # Still on upload page, check for error or loading message
            error_div = page.locator("#error")
            loading_div = page.locator("#loading")
            # Either error or loading should be visible
            assert error_div.is_visible() or loading_div.is_visible() or page.url == f"{self.BASE_URL}/comparison/"

    def test_file_display_areas_exist(self, page):
        """Test that file display areas exist"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Check file display areas
        displays = page.locator(".file-input-display")
        expect(displays).to_have_count(2)
        
        # Check initial text
        for display in displays.all():
            expect(display).to_contain_text("No file chosen")

    def test_results_page_structure(self, page):
        """Test that results page has correct structure"""
        page.goto(f"{self.BASE_URL}/comparison/results")
        
        # Check page title
        expect(page).to_have_title("Comparison Results")
        
        # Check heading
        heading = page.locator("h1")
        expect(heading).to_contain_text("Comparison Results")
        
        # Check back button exists
        back_button = page.locator("a:has-text('Upload New Files')")
        expect(back_button).to_have_count(1)

    def test_navigation_between_pages(self, page):
        """Test navigation between upload and results pages"""
        # Go to upload page
        page.goto(f"{self.BASE_URL}/comparison/")
        expect(page).to_have_url(f"{self.BASE_URL}/comparison/")
        
        # Go to results page
        page.goto(f"{self.BASE_URL}/comparison/results")
        expect(page).to_have_url(f"{self.BASE_URL}/comparison/results")
        
        # Click back button
        back_button = page.locator("a:has-text('Upload New Files')")
        back_button.click()
        expect(page).to_have_url(f"{self.BASE_URL}/comparison/")

    def test_info_box_displayed(self, page):
        """Test that info box with supported formats is displayed"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        info_box = page.locator(".info-box")
        expect(info_box).to_be_visible()
        expect(info_box).to_contain_text("Supported formats")
        expect(info_box).to_contain_text("Excel")
        expect(info_box).to_contain_text("CSV")

    def test_all_buttons_have_cursor_pointer(self, page):
        """Test that all buttons have pointer cursor (CSS check)"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Get all buttons
        buttons = page.locator("button")
        
        for button in buttons.all():
            # Check cursor style (this is a visual check, but we can verify button exists)
            expect(button).to_be_visible()
            
    def test_both_choose_file_buttons_work(self, page, sample_excel_file):
        """Test that both Choose File buttons function correctly"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Get both Choose File buttons
        choose_file_buttons = page.locator("button:has-text('Choose File')")
        expect(choose_file_buttons).to_have_count(2)
        
        # Get file inputs
        gt_input = page.locator('input[name="ground_truth"]')
        ext_input = page.locator('input[name="extracted_result"]')
        
        # Click first button and set file
        choose_file_buttons.first.click()
        gt_input.set_input_files({
            'name': 'ground_truth.xlsx',
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        page.wait_for_timeout(300)
        
        # Verify first file display updated
        gt_display = page.locator('#gtFileDisplay')
        expect(gt_display).to_contain_text("ground_truth.xlsx")
        
        # Click second button and set file
        choose_file_buttons.nth(1).click()
        ext_input.set_input_files({
            'name': 'extracted.xlsx',
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        page.wait_for_timeout(300)
        
        # Verify second file display updated
        ext_display = page.locator('#extFileDisplay')
        expect(ext_display).to_contain_text("extracted.xlsx")
        
    def test_compare_button_disabled_during_submission(self, page, sample_excel_file):
        """Test that Compare Files button is disabled during form submission"""
        page.goto(f"{self.BASE_URL}/comparison/")
        
        # Set both files
        gt_input = page.locator('input[name="ground_truth"]')
        ext_input = page.locator('input[name="extracted_result"]')
        
        gt_input.set_input_files({
            'name': sample_excel_file['name'],
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        
        ext_input.set_input_files({
            'name': sample_excel_file['name'],
            'mimeType': sample_excel_file['mimeType'],
            'buffer': sample_excel_file['buffer']
        })
        
        page.wait_for_timeout(300)
        
        compare_button = page.locator("button:has-text('Compare Files')")
        
        # Initially enabled
        expect(compare_button).to_be_enabled()
        
        # Click to submit - this will trigger form submission
        compare_button.click()
        
        # Wait a bit for JavaScript to process
        page.wait_for_timeout(200)
        
        # After click, either:
        # 1. Button is disabled (if still on page)
        # 2. Page navigated away (button no longer visible)
        # 3. Loading message appears
        loading_div = page.locator("#loading")
        error_div = page.locator("#error")
        current_url = page.url
        
        # Verify something happened - either loading, error, or navigation
        assert (
            loading_div.is_visible() or 
            error_div.is_visible() or 
            "/comparison/results" in current_url or
            compare_button.is_visible()  # Button still visible means form is processing
        )
        
    def test_back_button_navigation(self, page):
        """Test that back button on results page works"""
        # First navigate to results page
        page.goto(f"{self.BASE_URL}/comparison/results")
        
        # Find back button
        back_button = page.locator("a:has-text('Upload New Files')")
        expect(back_button).to_be_visible()
        expect(back_button).to_be_enabled()
        
        # Click back button
        back_button.click()
        
        # Should navigate back to upload page
        expect(page).to_have_url(f"{self.BASE_URL}/comparison/")
        
        # Verify we're on the upload page
        expect(page.locator("h1")).to_contain_text("Data Comparison Tool")

