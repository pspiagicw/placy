import { NavigationContainer } from "@react-navigation/native/"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import Auth from "../screens/Auth"
import { useSelector } from "react-redux";
import { Text } from "react-native-paper";
import { View } from "react-native";
import useAuthService from "../hooks/api/authService";
import { useEffect } from "react";
export default Routes = () => {

    const isLoading = useSelector(state => state.auth.isLoading);
    const isSignedIn = useSelector(state => state.auth.isLoggedIn);
    const AuthStack = createNativeStackNavigator();
    const AppStack = createNativeStackNavigator();

    const authService = useAuthService()

    useEffect(() => {
        authService.getUserFromToken()
    }, [])

    const AuthStackScreens = () => (
        <AuthStack.Navigator>
            <AuthStack.Screen name="Auth" component={Auth} />
        </AuthStack.Navigator>
    )

    const AppStackScreens = () => (
        <AppStack.Navigator>
            <AppStack.Screen name="Home" component={()=><View><Text>Hello</Text></View>}/>
        </AppStack.Navigator>
    )

    return (
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
    )
}