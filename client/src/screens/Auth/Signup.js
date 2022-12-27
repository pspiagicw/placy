import { TouchableOpacity, View, Text, TextInput } from 'react-native'
import React, { useRef, useState } from 'react'
import useAuthService from '../../hooks/api/authService'
import sharedStyles from './sharedStyles'

const Signup = ({ handleLoginInstead }) => {
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const authService = useAuthService()

    const handleSignup = () => {
        authService.signup(email, password)
    }

    const emailInputRef = useRef()
    const passwordInputRef = useRef()
    const confirmPasswordInputRef = useRef()

    return (
        <View style={sharedStyles.topContainer}>
            <Text style={sharedStyles.titleText}>Enter Name</Text>
            <TextInput
                style={sharedStyles.input}
                placeholder="Username"
                textContentType="name"
                autoCorrect={false}
                autoCapitalize="words"
                value={name}
                onChangeText={t => setName(t)}
                returnKeyType="next"
                onSubmitEditing={() => emailInputRef.current.focus()}
                blurOnSubmit={false}
            />
            <Text style={sharedStyles.titleText}>Enter Email Address</Text>
            <TextInput
                style={sharedStyles.input}
                placeholder="name@example.com"
                textContentType="emailAddress"
                autoCorrect={false}
                autoCapitalize="none"
                value={email}
                onChangeText={t => setEmail(t)}
                returnKeyType="next"
                onSubmitEditing={() => passwordInputRef.current.focus()}
                blurOnSubmit={false}
                ref={emailInputRef}
            />
            <Text style={sharedStyles.titleText}>Enter Password</Text>
            <TextInput
                secureTextEntry
                style={sharedStyles.input}
                placeholder="Password"
                textContentType="password"
                autoCorrect={false}
                autoCapitalize="none"
                value={password}
                onChangeText={t => setPassword(t)}
                onSubmitEditing={() => confirmPasswordInputRef.current.focus()}
                ref={passwordInputRef}
            />
            <Text style={sharedStyles.titleText}>Enter Password</Text>
            <TextInput
                secureTextEntry
                style={sharedStyles.input}
                placeholder="Password"
                textContentType="password"
                autoCorrect={false}
                autoCapitalize="none"
                value={confirmPassword}
                onChangeText={t => setConfirmPassword(t)}
                onSubmitEditing={handleSignup}
                ref={confirmPasswordInputRef}
            />
            <TouchableOpacity style={sharedStyles.button} onPress={handleSignup}>
                <Text style={sharedStyles.buttonText}>Signup</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={handleLoginInstead}>
                <Text style={sharedStyles.actionText}>Login Instead?</Text>
            </TouchableOpacity>
        </View>
    )
}

export default Signup
