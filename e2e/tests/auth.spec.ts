import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { TEST_USERS } from '../fixtures/test-data';

test.describe('Authentication', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('should display login form', async ({ page }) => {
    await expect(loginPage.emailInput).toBeVisible();
    await expect(loginPage.passwordInput).toBeVisible();
    await expect(loginPage.submitButton).toBeVisible();
    await expect(loginPage.registerLink).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await loginPage.login(TEST_USERS.invalid.email, TEST_USERS.invalid.password);
    
    // Check for error message (adjust selector based on your app)
    const errorMessage = page.locator('[data-testid="error"], .alert-error, .text-red-600');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Invalid credentials');
  });

  test('should navigate to register page', async ({ page }) => {
    await loginPage.register();
    await expect(page).toHaveURL('/register');
    
    // Check for register form
    const registerForm = page.locator('[data-testid="register-form"], form:has-text("Register")');
    await expect(registerForm).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    // Note: This test assumes you have a test user in the database
    // In a real setup, you might want to create a test user before this test
    
    await loginPage.login(TEST_USERS.existing.email, TEST_USERS.existing.password);
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Check for successful login indication
    const welcomeMessage = page.locator('[data-testid="welcome-message"], h1');
    await expect(welcomeMessage).toBeVisible();
  });

  test('should maintain session after page reload', async ({ page }) => {
    // Login first
    await loginPage.login(TEST_USERS.existing.email, TEST_USERS.existing.password);
    await expect(page).toHaveURL('/dashboard');
    
    // Reload page
    await page.reload();
    
    // Should still be logged in
    const welcomeMessage = page.locator('[data-testid="welcome-message"], h1');
    await expect(welcomeMessage).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await loginPage.login(TEST_USERS.existing.email, TEST_USERS.existing.password);
    await expect(page).toHaveURL('/dashboard');
    
    // Logout (adjust selector based on your app)
    const logoutButton = page.locator('button:has-text("Logout"), [data-testid="logout-btn"]');
    await logoutButton.click();
    
    // Should redirect to login page
    await expect(page).toHaveURL('/login');
  });
});