# Vercel Deployment

This project is now set up as a static Vercel app with small serverless API functions for the OTP mocks and Grid AI PAN extraction.

## Project settings

- Framework preset: Other
- Build command: leave empty
- Output directory: leave empty
- Install command: leave empty unless Vercel asks to install project tooling

Make sure Vercel's root directory is the repository/project root that contains `vercel.json`, `api/`, and `public/`. If the root directory is set to `demonstration/`, Vercel will miss the deployment config and the clean routes can return 404.

## Environment variables

Add these in Vercel Project Settings > Environment Variables:

- `GRID_AUTH_TOKEN`: required for PAN extraction
- `LITELLM_BASE_URL`: optional, defaults to `https://grid.ai.juspay.net`
- `GRID_MODEL`: optional, defaults to `kimi-latest`

## Routes

- `/` and `/otp` open the OTP screen.
- Other screens use clean routes such as `/eligibility-check`, `/choose-plan`, and `/all-set`.
- The AI endpoint is `/api/extract-pan`.
- Old `/api/demonstration/...` page and API URLs are still supported through Vercel rewrites.
