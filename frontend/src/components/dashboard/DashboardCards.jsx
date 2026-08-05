import { Grid } from "@mui/material";
import EventIcon from "@mui/icons-material/Event";
import DirectionsWalkIcon from "@mui/icons-material/DirectionsWalk";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import VideocamIcon from "@mui/icons-material/Videocam";

import StatCard from "./StatCard";

export default function DashboardCards() {
    return (
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
                <StatCard
                    title="Total Events"
                    value={124}
                    icon={<EventIcon />}
                    color="#2563EB"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
                <StatCard
                    title="Line Crossings"
                    value={31}
                    icon={<DirectionsWalkIcon />}
                    color="#22C55E"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
                <StatCard
                    title="Intrusions"
                    value={2}
                    icon={<WarningAmberIcon />}
                    color="#EF4444"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
                <StatCard
                    title="Active Cameras"
                    value={1}
                    icon={<VideocamIcon />}
                    color="#F59E0B"
                />
            </Grid>
        </Grid>
    );
}