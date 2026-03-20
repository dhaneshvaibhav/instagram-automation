# Frontend Documentation

The Reelzy Frontend is a modern, responsive React application built with **Vite**. It provides a premium "Studio" experience for managing Instagram automations.

## Core Technologies

- **React 18**: Component-based UI library.
- **Vite**: Ultra-fast build tool and development server.
- **React Router**: For client-side navigation (`/`, `/login`, `/dashboard`).
- **Axios**: For making RESTful API calls to the backend.
- **Lucide React**: For a consistent and modern icon set.

## Navigation & Routing

Routing is managed in [App.jsx](file:///c:/Users/Dell/OneDrive/Desktop/Coding/side-hustle/instagram%20automation/frontend/src/App.jsx).

- **`/` (LandingPage)**: Public marketing page.
- **`/login` (Login)**: Authentication entry point.
- **`/dashboard` (Dashboard)**: Protected route (requires an active Instagram connection).

## API Integration

The frontend communicates with the backend via a pre-configured Axios instance in [api.js](file:///c:/Users/Dell/OneDrive/Desktop/Coding/side-hustle/instagram%20automation/frontend/src/api.js).

- **Environment Variable**: `VITE_API_URL` defines the backend endpoint.
- **WithCredentials**: Set to `true` to allow secure cookie-based session sharing between frontend and backend.

## Component Breakdown

### 1. Dashboard (`Dashboard.jsx`)
The main workspace for managing automations. It orchestrates the layout, stats, and live activity logs.

### 2. Stats (`Stats.jsx`)
Displays real-time metrics (Total Reels, DMs sent today, Total DMs) fetched from the backend.

### 3. Reels List (`ReelsList.jsx`)
Renders all active automation rules. It includes:
- **Visual Feedback**: Shows icons for URL and Postback buttons.
- **Test Actions**: A "Test" button to trigger a manual DM to the authenticated user.
- **Delete Actions**: For stopping automation on a specific Reel.

### 4. Add Reel Form (`AddReelForm.jsx`)
A dynamic form for creating automation rules.
- **Max 3 Buttons**: Allows users to add interactive URL or Postback buttons.
- **Selection**: Integrated with the Media Gallery for easy Reel picking.

### 5. Media Gallery (`MediaGallery.jsx`)
Fetches and displays the user's actual Instagram Reels as a grid of thumbnails. This improves UX by avoiding manual Reel ID entry.

### 6. Log Viewer (`LogViewer.jsx`)
A real-time terminal that displays server activity logs. It auto-scrolls to the bottom and differentiates between success (Green) and error (Red) states.

## Styling & Design System

The app follows a **Glassmorphism / Dark Mode** aesthetic, defined in [index.css](file:///c:/Users/Dell/OneDrive/Desktop/Coding/side-hustle/instagram%20automation/frontend/src/index.css).

- **CSS Variables**: All colors, spacing, and radius values are centralized in `:root`.
- **Animations**: Uses custom `@keyframes` (`fadeIn`, `slideInRight`) for a fluid experience.
- **Glass Cards**: Cards use semi-transparent backgrounds and subtle borders for a modern look.

## Build & Deployment

To build the frontend for production:
```bash
cd frontend
npm run build
```
This generates a `dist/` folder which can be hosted on static platforms like **Vercel**, **Netlify**, or **Cloudflare Pages**.
