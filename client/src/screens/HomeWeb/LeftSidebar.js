import React from 'react'
import { Image, StyleSheet, Text, TouchableOpacity, View, ScrollView, FlatList, Dimensions } from 'react-native'
import { Entypo, Ionicons, MaterialCommunityIcons, Octicons, MaterialIcons } from '@expo/vector-icons'
import colors from '../../theme/colors'

const Tab = ({ name, icon, onPress = () => { }, styles }) => {
  return <TouchableOpacity onPress={onPress} activeOpacity={0.7} style={{ backgroundColor: 'yellow', height: 50, marginVertical: 10, alignItems: 'center', flexDirection: 'row', ...styles }}>
    {icon}
    <Text style={{ marginLeft: 10 }} >{name}</Text>
  </TouchableOpacity>
}

const QuestionContainer = () => {
  const questions = [
    // { name: "Internships", id: 1, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 2, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 3, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 4, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 5, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 6, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 7, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 8, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions 9", id: 9, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 10, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 11, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions", id: 12, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
    { name: "Previously asked questions 13", id: 13, onPress: () => { }, image: "https://winaero.com/blog/wp-content/uploads/2019/11/Photos-new-icon.png" },
  ];


  return (
    <View style={{ marginBottom: 10, flex: 1 }}>
      <View style={{ backgroundColor: 'yellow', height: 50, alignItems: 'center', flexDirection: 'row', marginTop: 10, }}>
        <MaterialCommunityIcons name="frequently-asked-questions" size={24} color='black' />
        <Text style={{ marginLeft: 10 }}>Questions</Text>
      </View>
      <FlatList
        // style={{ height: '100%' }}
        data={questions}
        renderItem={({ item }) =>
          <Tab
            key={item.id}
            name={item.name}
            onPress={item.onPress}
            styles={{ marginLeft: 10, marginVertical: 0, marginTop: 10, }}
            icon={<Image source={{ uri: item.image }} style={{ height: 24, width: 24, }} />}
          />}
        keyExtractor={item => item.id}
      />
    </View>)
}



const LeftSidebar = () => {
  return (
    <View style={{ backgroundColor: "red", height: '100%' }}>
      <View>
      <Tab name="Placy" icon={<MaterialCommunityIcons name="book-education" size={24} color="black" />} />
      
        <Tab name="Announcements" icon={<Entypo name="megaphone" size={24} color="black" />} />
        <Tab name="Mailbox" icon={<Entypo name="mail" size={24} color="black" />} />
        <Tab name="Internship" icon={<MaterialIcons name="work" size={24} color="black" />} />
        <Tab name="Forum/Discuss" icon={<Octicons name="feed-discussion" size={24} color="black" />} />
      </View>
      <QuestionContainer />
      <Tab name="Settings" icon={<Ionicons name="settings" size={24} color='black' />} />
    </View>
  )
}

export default LeftSidebar

const styles = StyleSheet.create({})