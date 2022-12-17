import { Platform, StyleSheet, TouchableOpacity, View } from 'react-native'
import React, { useEffect, useState } from 'react'
import { Text, TextInput, Button } from 'react-native-paper'
import useAuthService from '../../hooks/api/authService'
import colors from '../../theme/colors'

const Auth = ({ navigation }) => {
    const [isLoggingIn, setIsLoggingIn] = useState(true)
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const authService = useAuthService()

    const handleSignup = () => {
        authService.signup(email, password)
    }

    const handleLogin = () => {
        authService.signup(email, password)
    }

    return (
        <View style={styles.container}>
            <View>
                <Text variant='headlineLarge'>{isLoggingIn ? "Log in" : "Sign up"}</Text>
            </View>
            <View style={styles.fieldsContainer}>
                <View>
                    <Text variant='labelLarge' >Email address</Text>
                    <TextInput label="Email" textContentType='emailAddress' autoComplete='email' autoCapitalize='none' value={email} onChangeText={v => setEmail(v)} left={<TextInput.Icon icon={'email'} />} />
                </View>
                <View>
                    <Text>Password</Text>
                    <TextInput label="Password" secureTextEntry={true} value={password} onChangeText={v => setPassword(v)} left={<TextInput.Icon icon={'lock'} />} />
                </View>
                <Button mode='elevated' onPress={isLoggingIn ? handleLogin : handleSignup}>{isLoggingIn ? "signin" : "signup"}</Button>
                <Text>Don't have an account?
                    <TouchableOpacity onPress={() => setIsLoggingIn(!isLoggingIn)}><Text>Signup</Text></TouchableOpacity>
                </Text>

                <TouchableOpacity onPress={() => navigation.navigate("Forgot")}><Text style={{ color: colors.primary }}>Forgot password?</Text></TouchableOpacity>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        display: 'flex',
    },
    fieldsContainer: {
        display: 'flex',
        flexDirection: 'column',
    }
})

export default Auth