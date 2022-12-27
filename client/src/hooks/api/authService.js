import { getAuthenticatedAxios, getUnauthenticatedAxios } from "./baseConfig"
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useDispatch, useSelector } from "react-redux"
import { loginUser, logoutUser, setLoaded, setLoading } from "../../store/reducers/authSlice"
import { useEffect } from "react"


const useAuthService = () => {
    const dispatch = useDispatch()

    const tokenFromStore = useSelector(state => state.auth.token)

    const signup = async (email, password) => {
        try {
            const unauthenticatedAxios = getUnauthenticatedAxios('/auth')
            // const data = await unauthenticatedAxios.post('/signup', { email, password });
            const data = { token: Math.random().toString() }
            const token = data['token'];
            dispatch(loginUser(token))
            return token;
        } catch (error) {
            throw error;
        }
    }

    const logout = () => {
        dispatch(logoutUser())
    }

    const mockDelayedResolve = (cb, timeout) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                return resolve(cb)
            }, timeout);
        })
    }

    const forgot = async (email) => {

    }

    const reset = async (email, otp, password) => {
        alert("Reset")

    }

    const getUserFromToken = async () => {
        try {
            dispatch(setLoading())
            const token = await AsyncStorage.getItem('@token');
            if (!token) return;
            const authenticatedAxios = getAuthenticatedAxios('/users', token);
            // const user = await (await authenticatedAxios.get('/me')).data['user'];
            const user = { role: "user", email: "test@example.com", exp: 1666073513.056, iat: 1666044713 }
            // await mockDelayedResolve(() => { }, 500)
            dispatch(loginUser(token))
            return user;
        } catch (error) {
            throw error;
        }
        finally {
            dispatch(setLoaded())
        }
    }



    return { signup, logout, forgot, reset, getUserFromToken, token: tokenFromStore }

}

export default useAuthService;