import { StyleSheet, Text, View } from 'react-native';
import React, { useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useDispatch } from 'react-redux';
import { logoutUser } from '../../store/reducers/authSlice';
import { Button } from 'react-native-paper';
import useAuthService from '../../hooks/api/authService';
import Feed from '../../components/Feed';

const Discover = () => {
   const authService = useAuthService();
   const [tokenFromStorage, setTokenFromStorage] = useState('');
   AsyncStorage.getItem('@token').then(token => setTokenFromStorage(token));

   const dispatch = useDispatch();

   return (
      <View>
         <Feed />
         <Feed />
         <Feed />
         <Text>token from store {authService.token}</Text>
         <Text>token from storage {tokenFromStorage}</Text>
         <Button onPress={() => dispatch(logoutUser())}>
            <Text>Logout</Text>
         </Button>
      </View>
   );
};

export default Discover;

const styles = StyleSheet.create({});
