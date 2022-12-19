import { StyleSheet, Text, View } from 'react-native'
import React from 'react'

const SearchBar = () => {
    return <View style={{ height: 50, backgroundColor: 'blue', flexDirection: 'row', alignItems: 'center' }}>
        <Text>SearchBar</Text>
    </View>
}
const RightSidebar = () => {

    return (
        <View style={{ flex: 1, backgroundColor: "red" }}>
            <SearchBar />
            <Text>RightSidebar</Text>
        </View>
    )
}

export default RightSidebar

const styles = StyleSheet.create({})