import { useEffect } from "react";
import { TouchableOpacity, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native/"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { SafeAreaProvider } from "react-native-safe-area-context";
import { Button, Text } from "react-native-paper";
import { useDispatch, useSelector } from "react-redux";
import useAuthService from "../hooks/api/authService";
import Auth from "../screens/Auth"
import { logoutUser } from "../store/reducers/authSlice";


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

    const TempHomeScreen = () => (
        <View><Text>Hello</Text><Button onPress={() => dispatch(logoutUser())}><Text>Logout</Text></Button></View>
    )
    const AppStackScreens = () => (
        <AppStack.Navigator>
            <AppStack.Screen name="Home" component={TempHomeScreen} />
        </AppStack.Navigator>
    )

    return (
        <SafeAreaProvider>
            <NavigationContainer>
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