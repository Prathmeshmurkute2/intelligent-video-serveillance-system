import NotificationsIcon from "@mui/icons-material/Notifications";
import {
    AppBar,
    Avatar,
    Badge,
    Box,
    IconButton,
    Toolbar,
    Typography,
} from "@mui/material";

const drawerWidth = 240;

export default function Navbar() {
    return (
        <AppBar
            position="fixed"
            elevation={1}
            sx={{
                width: `calc(100% - ${drawerWidth}px)`,
                ml: `${drawerWidth}px`,
                bgcolor: "#FFFFFF",
                color: "#1E293B",
            }}
        >
            <Toolbar>

                <Typography
                    variant="h6"
                    fontWeight="bold"
                    sx={{ flexGrow: 1 }}
                >
                    Intelligent Video Surveillance
                </Typography>

                <IconButton color="inherit">
                    <Badge
                        badgeContent={3}
                        color="error"
                    >
                        <NotificationsIcon />
                    </Badge>
                </IconButton>

                <Box
                    display="flex"
                    alignItems="center"
                    ml={2}
                >
                    <Avatar
                        sx={{
                            bgcolor: "#2563EB",
                        }}
                    >
                        A
                    </Avatar>

                    <Typography
                        ml={1}
                        fontWeight="500"
                    >
                        Admin
                    </Typography>
                </Box>

            </Toolbar>
        </AppBar>
    );
}