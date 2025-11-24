# Resume Upload Bug - Fix Documentation

## Root Cause

When you upload a resume via the UI Profile modal, the system:

1. ✅ Uploads the resume successfully (extracts text, saves to `user_profile.json`)
2. ❌ **THEN immediately saves the profile from the textarea**, which overwrites the resume with OLD data

**The bug is in** `frontend/index.html` **line 696-700**:

After uploading the resume, the frontend ALWAYS calls `POST /profile` with the data from the textarea.  
The textarea contains the OLD profile (with empty or old `resume_text`), so it overwrites the freshly uploaded resume!

## The Fix

After resume upload succeeds, we need to **re-fetch the profile** to get the updated `resume_text` before saving the profile.

### Manual Fix Steps

1. Open `frontend/index.html`
2. Find line 687: `profileStatus.innerText = 'Resume uploaded successfully!';`
3. **Add this code RIGHT AFTER line 687**:

```javascript
            // CRITICAL FIX: Re-fetch profile to get the updated resume_text
            // Otherwise the next profile save will overwrite it with old data
            try {
              const refreshRes = await fetch('http://127.0.0.1:5050/profile');
              const refreshedProfile = await refreshRes.json();
              // Merge new resume_text into parsed data
              parsed.resume_text = refreshedProfile.resume_text || '';
              console.log('Refreshed profile - resume length:', parsed.resume_text.length);
            } catch (refreshErr) {
              console.warn('Failed to refresh profile:', refreshErr);
            }
```

4. Save the file
5. Restart the frontend app

### After the Fix

When you upload a resume:
1. Resume uploads → extracts 22,980 characters
2. Profile refreshes → gets the new resume from backend
3. Profile saves → preserves the new resume (doesn't overwrite it)

## Testing

1. Upload `Milan Barot_test.docx` (with PhD education)
2. Check backend console:
   ```
   [SAVE_PROFILE] Successfully wrote XXXX bytes  (resume upload)
   Refreshed profile - resume length: 22980      (profile refresh - NEW!)
   [SAVE_PROFILE] Successfully wrote XXXX bytes  (profile save - preserves resume)
   ```
3. Ask "What's your education?"
4. AI should mention PhD, not Bachelor's

## Current Workaround

Until the fix is applied:
- **Don't use the UI to upload resumes**
- Use the script instead:
  ```bash
  cd "c:\Data Engineering\codeprep\interview_assistant\backend"
  python process_resume.py "C:\path\to\your\resume.docx"
  ```
- The script directly updates the file and doesn't trigger the overwrite bug

## Why Auto-Edits Failed

Automated file replacement tools kept breaking the HTML/JavaScript structure.  
Manual editing is safer for this complex JavaScript code.
