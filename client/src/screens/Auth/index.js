import { StyleSheet, TouchableOpacity, View, Text, TextInput } from 'react-native'
import React, { useEffect, useState } from 'react'
import useAuthService from '../../hooks/api/authService'
import sharedStyles from './sharedStyles'

import Login from './Login'
import Signup from './Signup'

const Auth = ({ navigation }) => {
    const [isLoggingIn, setIsLoggingIn] = useState(true)
    const authService = useAuthService()

    const handleSignup = () => {
        authService.signup(email, password)
    }

    return (
        // <View style={styles.container}>
        //     <View>
        //         <Text variant='headlineLarge'>{isLoggingIn ? "Log in" : "Sign up"}</Text>
        //     </View>
        //     <View style={styles.fieldsContainer}>
        //         <View>
        //             <Text variant='labelLarge' >Email address</Text>
        //             <TextInput label="Email" textContentType='emailAddress' autoComplete='email' autoCapitalize='none' value={email} onChangeText={v => setEmail(v)} left={<TextInput.Icon icon={'email'} />} />
        //         </View>
        //         <View>
        //             <Text>Password</Text>
        //             <TextInput label="Password" secureTextEntry={true} value={password} onChangeText={v => setPassword(v)} left={<TextInput.Icon icon={'lock'} />} />
        //         </View>
        //         <Button mode='elevated' onPress={isLoggingIn ? handleLogin : handleSignup}>{isLoggingIn ? "signin" : "signup"}</Button>
        //         <Text>Don't have an account?
        //             <TouchableOpacity onPress={() => setIsLoggingIn(!isLoggingIn)}><Text>Signup</Text></TouchableOpacity>
        //         </Text>

        //         <TouchableOpacity onPress={() => navigation.navigate("Forgot")}><Text style={{ color: colors.primary }}>Forgot password?</Text></TouchableOpacity>
        //     </View>
        // </View>
        <View style={sharedStyles.container}>
            {isLoggingIn
                ? <Login
                    handleForgotPassword={() => navigation.navigate("Forgot")}
                    handleSignupInstead={() => { setIsLoggingIn(false) }}
                />
                : <Signup
                    handleLoginInstead={() => { setIsLoggingIn(true) }}
                />}
        </View>
    )
}

const styles = StyleSheet.create({

})

export default Auth
