import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Calendar } from 'react-calendar'
import './Calendar.css'

const RightSidebar = () => {

    return (
        <View style={{ flex: 1, alignItems: 'center' }}>
            <Text style={{ fontWeight: '600', fontSize: 20, marginBottom: 10 }}>Schedule</Text>
            <Calendar />
        </View>
    )
}

export default RightSidebar

const styles = StyleSheet.create({})