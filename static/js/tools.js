document.addEventListener('DOMContentLoaded', function() {
    // Password Generator
    const generatePassword = document.getElementById('generatePassword');
    const passwordLength = document.getElementById('passwordLength');
    const includeNumbers = document.getElementById('includeNumbers');
    const includeSymbols = document.getElementById('includeSymbols');
    const generatedPassword = document.getElementById('generatedPassword');

    function generateRandomPassword(length, numbers, symbols) {
        const letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';
        const syms = '!@#$%^&*()_+-=[]{}|;:,.<>?';

        let chars = letters;
        if (numbers) chars += nums;
        if (symbols) chars += syms;

        let password = '';
        for (let i = 0; i < length; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        return password;
    }

    generatePassword.addEventListener('click', function() {
        const length = parseInt(passwordLength.value);
        const useNumbers = includeNumbers.checked;
        const useSymbols = includeSymbols.checked;

        const password = generateRandomPassword(length, useNumbers, useSymbols);
        generatedPassword.value = password;
    });

    // URL Scanner
    const scanUrl = document.getElementById('scanUrl');
    const urlToScan = document.getElementById('urlToScan');
    const scanResult = document.getElementById('scanResult');

    scanUrl.addEventListener('click', async function() {
        const url = urlToScan.value.trim();
        if (!url) {
            scanResult.innerHTML = '<div class="alert alert-warning">Please enter a URL</div>';
            return;
        }

        scanResult.innerHTML = '<div class="alert alert-info">Scanning URL...</div>';
        
        try {
            const response = await fetch('/scan-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            
            const data = await response.json();
            
            if (data.safe) {
                scanResult.innerHTML = '<div class="alert alert-success">This URL appears to be safe</div>';
            } else {
                scanResult.innerHTML = '<div class="alert alert-danger">This URL might be malicious</div>';
            }
        } catch (error) {
            scanResult.innerHTML = '<div class="alert alert-danger">Error scanning URL</div>';
        }
    });
});
