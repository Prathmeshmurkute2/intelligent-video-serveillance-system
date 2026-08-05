import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";

import Dashboard from "../pages/Dashboard.jsx";
import Events from "../pages/Events.jsx";
import Cameras from "../pages/Cameras.jsx";
import Login from "../pages/Login.jsx";
import Settings from "../pages/Settings.jsx";

export default function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>

                <Route path="/login" element={<Login />} />

                <Route element={<DashboardLayout />}>

                    <Route path="/" element={<Dashboard />} />

                    <Route path="/events" element={<Events />} />

                    <Route path="/cameras" element={<Cameras />} />

                    <Route path="/settings" element={<Settings />} />

                </Route>

            </Routes>
        </BrowserRouter>
    );
}