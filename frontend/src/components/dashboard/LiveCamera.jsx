import { useState } from "react";
import {
    Paper,
    Typography,
    Button,
    Box,
} from "@mui/material";

export default function LiveCamera() {

    const [running, setRunning] = useState(false);
    const [loading, setLoading] = useState(false);

    const startCamera = async () => {

        setLoading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/camera/start",
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to start camera");
            }

            setRunning(true);

        } catch (error) {

            console.error(
                "❌ Failed to start camera:",
                error
            );

        } finally {

            setLoading(false);
        }
    };


    const stopCamera = async () => {

        setLoading(true);

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/camera/stop",
                {
                    method: "POST",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to stop camera");
            }

            setRunning(false);

        } catch (error) {

            console.error(
                "❌ Failed to stop camera:",
                error
            );

        } finally {

            setLoading(false);
        }
    };


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


            {/* Camera controls */}

            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 2,
                    mb: 2,
                }}
            >

                <Button
                    variant="contained"
                    color="success"
                    onClick={startCamera}
                    disabled={running || loading}
                >
                    ▶ Start Camera
                </Button>


                <Button
                    variant="contained"
                    color="error"
                    onClick={stopCamera}
                    disabled={!running || loading}
                >
                    ■ Stop Camera
                </Button>


                <Typography
                    fontWeight="bold"
                    sx={{
                        ml: 1,
                    }}
                >
                    {running
                        ? "🟢 Camera Running"
                        : "🔴 Camera Stopped"}
                </Typography>

            </Box>


            {/* Camera stream */}

            {running && (

                <img
                    src="http://127.0.0.1:8000/camera/stream"
                    alt="Live Camera"
                    style={{
                        width: "100%",
                        borderRadius: "12px",
                    }}
                />

            )}

        </Paper>
    );
}