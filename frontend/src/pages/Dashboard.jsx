import DashboardCards from "../components/dashboard/DashboardCards";
import RecentEvents from "../components/dashboard/RecentEvents";
import EventChart from "../components/dashboard/EventChart";
import LiveCamera from "../components/dashboard/LiveCamera";

import { useDashboard } from "../hooks/useDashboard";
import { useWebSocket } from "../hooks/useWebSocket";

export default function Dashboard() {

    const { data, isLoading, error } = useDashboard();

    useWebSocket((message) => {

        switch (message.type) {

            case "event_created":

                console.log("New Event:", message.data);

                break;

            default:

                console.log(message);

                break;
        }

    });

    if (isLoading) return <h2>Loading...</h2>;

    if (error) return <h2>Something went wrong.</h2>;

    return (
        <>
            <DashboardCards
                analytics={data.data.analytics}
            />

            <EventChart />

            <LiveCamera />

            <RecentEvents
                events={data.data.recent_events}
            />
        </>
    );
}