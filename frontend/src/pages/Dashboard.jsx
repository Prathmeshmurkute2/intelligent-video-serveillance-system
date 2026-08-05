import DashboardCards from "../components/dashboard/DashboardCards.jsx";

import { useDashboard } from "../hooks/useDashboard.js";

export default function Dashboard() {

    const { data, isLoading, error } = useDashboard();

    if (isLoading) {
        return <h2>Loading...</h2>;
    }

    if (error) {
        return <h2>Something went wrong.</h2>;
    }

    console.log(data);

    return (
        <>
            <DashboardCards />
        </>
    );
}