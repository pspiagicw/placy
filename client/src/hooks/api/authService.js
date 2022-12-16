import { getAuthenticatedAxios, getUnauthenticatedAxios } from "./baseConfig"
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useDispatch, useSelector } from "react-redux"
import { loginUser, setLoaded } from "../../store/reducers/authSlice"


const useAuthService = () => {
    const dispatch = useDispatch()
    const signup = async (email, password) => {
        try {
            const unauthenticatedAxios = getUnauthenticatedAxios('/auth')
            // const data = await unauthenticatedAxios.post('/signup', { email, password });
            const data = { token: Math.random().toString() }
            const token = data['token'];
            await AsyncStorage.setItem('@token', token);
            dispatch(loginUser(token))
            return token;
        } catch (error) {
            throw error;
        }
    }

    const getUserFromToken = async () => {
        try {
            const token = await AsyncStorage.getItem('@token');
            if (token == null) return;
            const authenticatedAxios = getAuthenticatedAxios('/users', token);
            // const user = await (await authenticatedAxios.get('/me')).data['user'];
            const user = { role: "user", email: "test@example.com", exp: 1666073513.056, iat: 1666044713 }
            dispatch(loginUser(token))
            return user;
        } catch (error) {
            throw error;
        }
        finally {
            setTimeout(() => {
                dispatch(setLoaded())
            }, 400);
        }
    }



    return { signup, getUserFromToken }

}

export default useAuthService;