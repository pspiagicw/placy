import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./reducers/authSlice";
import communityReducer from "./reducers/communitySlice";

export default configureStore({
  reducer: {
    auth: authReducer,
    community: communityReducer
  },
});
