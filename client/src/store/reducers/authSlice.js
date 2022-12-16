import { createSlice } from "@reduxjs/toolkit";

export const authSlice = createSlice({
    name: "auth",
    initialState: {
        token: "",
        isLoading: true,
        isLoggedIn: false
    },
    reducers: {
        setToken: (state, action) => {
            state.token = action.payload
        },
        loginUser: (state) => {
            state.isLoggedIn = true
            state.isLoading = false;
        },
        logoutUser: (state) => {
            state.isLoggedIn = false;
        },
        setLoaded: (state) => {
            state.isLoading = false;
        },
        setLoading: (state) => {
            state.isLoading = true;
        }
    }
})
export const { setToken, loginUser, logoutUser, setLoaded, setLoading } = authSlice.actions

export default authSlice.reducer