import { useEffect, useState } from "react";
import { View } from "react-native";
import { NavigationContainer } from "@react-navigation/native/"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { SafeAreaProvider } from "react-native-safe-area-context";
import { Button, Text } from "react-native-paper";
import { useDispatch, useSelector } from "react-redux";
import useAuthService from "../hooks/api/authService";
import Auth from "../screens/Auth"
import { logoutUser } from "../store/reducers/authSlice";
import linking from "./linking";
import AsyncStorage from "@react-native-async-storage/async-storage";


const Routes = () => {

    const isLoading = useSelector(state => state.auth.isLoading);
    const isSignedIn = useSelector(state => state.auth.isLoggedIn);
    const AuthStack = createNativeStackNavigator();
    const AppStack = createNativeStackNavigator();

    const authService = useAuthService()

    const dispatch = useDispatch()

    useEffect(() => {
        authService.getUserFromToken()
    }, [])

    const AuthStackScreens = () => (
        <AuthStack.Navigator>
            <AuthStack.Screen name="Auth" component={Auth} />
        </AuthStack.Navigator>
    )

    const TempHomeScreen = () => {
        const [tokenFromStorage, setTokenFromStorage] = useState('')
        AsyncStorage.getItem('@token').then(token => setTokenFromStorage(token));

        return (<View>
            <Text>Hello</Text>
            <Button onPress={() => dispatch(logoutUser())}><Text>Logout</Text></Button>
            <Text>token from store {authService.token}</Text>
            <Text>token from storage {tokenFromStorage}</Text>
        </View>)
    }
    const AppStackScreens = () => (
        <AppStack.Navigator>
            <AppStack.Screen name="Home" component={TempHomeScreen} />
        </AppStack.Navigator>
    )

    return (
        <SafeAreaProvider>
            <NavigationContainer linking={linking}>
                <View style={{ flex: 1 }}>
                    {
                        isLoading &&
                        <View style={{ display: 'flex', flex: 1, justifyContent: 'center' }}>
                            <Text style={{ textAlign: 'center', }}>Loading....</Text>
                        </View>
                    }
                    {!isLoading && !isSignedIn && <AuthStackScreens />}
                    {!isLoading && isSignedIn && <AppStackScreens />}
                </View>
            </NavigationContainer>
        </SafeAreaProvider>
    )
}

export default Routes