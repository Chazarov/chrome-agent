import React from "react";
import ReactDOM from "react-dom/client";
import { HashRouter, Route, Routes } from "react-router-dom";
import { CookieConsentProvider } from "./context/CookieConsentContext.jsx";
import CookieBanner from "./components/CookieBanner.jsx";
import ExternalFontsLoader from "./components/ExternalFontsLoader.jsx";
import SiteLayout from "./components/SiteLayout.jsx";
import HomePage from "./pages/HomePage.jsx";
import PrivacyPolicyPage from "./pages/PrivacyPolicyPage.jsx";
import CookiePolicyPage from "./pages/CookiePolicyPage.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <CookieConsentProvider>
      <HashRouter>
        <ExternalFontsLoader />
        <CookieBanner />
        <Routes>
          <Route element={<SiteLayout />}>
            <Route index element={<HomePage />} />
            <Route path="privacy" element={<PrivacyPolicyPage />} />
            <Route path="cookies" element={<CookiePolicyPage />} />
          </Route>
        </Routes>
      </HashRouter>
    </CookieConsentProvider>
  </React.StrictMode>
);
