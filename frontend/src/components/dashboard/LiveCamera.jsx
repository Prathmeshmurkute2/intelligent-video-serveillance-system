import { Paper, Typography } from "@mui/material";

export default function LiveCamera() {
    return (
        <Paper
            elevation={3}
            sx={{
                mt: 4,
                p: 2,
                borderRadius: 3,
            }}
        >
            <Typography
                variant="h6"
                fontWeight="bold"
                mb={2}
            >
                Live Camera Feed
            </Typography>

            <img
                src="http://127.0.0.1:8000/camera/stream"
                alt="Live Camera"
                style={{
                    width: "100%",
                    borderRadius: "12px",
                }}
            />
        </Paper>
    );
}