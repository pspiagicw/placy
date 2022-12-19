import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import Feed from '../../components/Feed'

const MainFeed = () => {
    return (
        <View style={{ flex: 1, backgroundColor: 'yellow' }}>
            <Feed />
            <Feed />
            <Feed />
            <Feed />
        </View>
    )
}

export default MainFeed

const styles = StyleSheet.create({})