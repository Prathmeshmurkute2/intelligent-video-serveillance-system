import { Outlet } from "react-router-dom";

export default function DashboardLayout(){
    return (
        <div>
            Sidebar
            Navbar
           
           <Outlet />
        </div>
    )
}