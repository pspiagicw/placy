import { useEffect } from "react";
import { View } from "react-native";
import { NavigationContainer } from "@react-navigation/native/"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { SafeAreaProvider } from "react-native-safe-area-context";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createDrawerNavigator } from "@react-navigation/drawer";
import { Text } from "react-native-paper";
import { useDispatch, useSelector } from "react-redux";
import { Entypo, Ionicons } from "@expo/vector-icons";
import Auth from "../screens/Auth"
import useAuthService from "../hooks/api/authService";
import linking from "./linking";
import CustomDrawer from "./Drawer";
import colors from "../theme/colors";
import Discover from "../screens/Discover";


const Routes = () => {

    const isLoading = useSelector(state => state.auth.isLoading);
    const isSignedIn = useSelector(state => state.auth.isLoggedIn);
    const AuthStack = createNativeStackNavigator();
    const Tab = createBottomTabNavigator();
    const Drawer = createDrawerNavigator();

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

    const HomeStack = () => (
        <Drawer.Navigator drawerContent={props => {
            const filteredProps = { ...props, state: { ...props.state, routeNames: props.state.routeNames.filter((routeName) => { routeName !== 'Discover' }), routes: props.state.routes.filter((route) => route.name !== "Discover") } }
            return <CustomDrawer {...filteredProps} />
        }}>
            <Drawer.Screen name="Discover" component={Discover} />
        </Drawer.Navigator>
    )

    const Screen = () => <View><Text>index</Text></View>

    const TabScreens = () => (
        <Tab.Navigator screenOptions={({ route }) => ({
            tabBarIcon: ({ focused }) => {
                let icon;
                if (route.name === "Home") {
                    icon = <Entypo name="home" size={24} color={focused ? colors.primary : colors.secondary} />
                }
                else if (route.name === "Announcement") {
                    icon = <Entypo name="megaphone" size={24} color={focused ? colors.primary : colors.secondary} />
                }
                else if (route.name === "Settings") {
                    icon = <Ionicons name="settings" size={24} color={focused ? colors.primary : colors.secondary} />
                }
                return icon;
            }
        })}
        >
            <Tab.Screen name="Home" component={HomeStack} options={{ headerShown: false }} />
            <Tab.Screen name="Announcement" component={Screen} />
            <Tab.Screen name="Settings" component={Screen} />
        </Tab.Navigator>
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
                    {!isLoading && isSignedIn && <TabScreens />}
                </View>
            </NavigationContainer>
        </SafeAreaProvider>
    )
}

export default Routes