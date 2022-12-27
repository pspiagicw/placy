import { createSlice } from "@reduxjs/toolkit";

export const communitySlice = createSlice({
    name: "community",
    initialState: {},
    reducers: {
        trendingCommunities: [],
        subscribedCommunities: []
    },
})

export const { } = communitySlice.actions

export default communitySlice.reducer