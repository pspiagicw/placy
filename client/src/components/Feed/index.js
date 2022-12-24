import { FlatList, StyleSheet, Text, View, Image, TouchableOpacity, Platform } from 'react-native'
import React from 'react'
import { Entypo, Ionicons } from '@expo/vector-icons'
import colors from '../../theme/colors'
import Scrollbars from 'react-custom-scrollbars'

const Feed = (props) => {
    const renderPost = ({ item }) => (
        <View style={postStyles.container}>
            <View style={postStyles.headerContainer}>
                <Image style={postStyles.profilePhoto} source={{ uri: item.user.profilePhotoUrl }} />
                <View style={postStyles.infoContainer}>
                    <Text style={{ fontSize: 16, margin: 0, padding: 0, color: '#0f0f0f' }}>{item.user.username}</Text>
                    <Text style={{ fontSize: 11, ...margin(4, 0, 0, 0), padding: 0, color: colors.tertiary }}>{item.postedAt}</Text>
                </View>
                <TouchableOpacity style={postStyles.PostOptions}>
                    <Entypo name="dots-three-horizontal" size={16} color={colors.secondary} />
                </TouchableOpacity>
            </View>
            <View style={postStyles.post}>
                <Text>{item.post}</Text>
                <Image style={postStyles.image} source={{ uri: item.photoUrl }} />
                <View style={postStyles.details}>
                    <View style={postStyles.likes}>
                        <TouchableOpacity>
                            <Ionicons name="ios-heart-outline" size={24} color={colors.secondary} />
                        </TouchableOpacity>
                        <Text style={{ fontSize: 11, ...margin(0, 0, 0, 8), padding: 0, color: '#0f0f0f' }}>{item.likes}</Text>
                    </View>
                    <View style={postStyles.comments}>
                        <TouchableOpacity>
                            <Ionicons name="ios-chatbox-outline" size={24} color={colors.secondary} />
                        </TouchableOpacity>
                        <Text style={{ fontSize: 11, ...margin(0, 0, 0, 8), padding: 0, color: '#0f0f0f' }}>{item.comments}</Text>
                    </View>
                </View>
            </View>
        </View>
    )

    return (
        <View style={postStyles.Container}>
            {Platform.OS == 'web' ?
                <Scrollbars>
                    <FlatList data={props.feedData} renderItem={renderPost} keyExtractor={item => item.id.toString()} />
                </Scrollbars> :
                <FlatList overScrollMode='never' data={props.feedData} renderItem={renderPost} keyExtractor={item => item.id.toString()} />
            }
        </View>
    )
}

export default Feed;

const margin = (a, b, c, d) => ({
    marginTop: a,
    marginRight: b ?? a,
    marginBottom: c ?? a,
    marginLeft: d ?? b ?? a,
})

const postStyles = StyleSheet.create({
    Container: {
        flex: 1,
        backgroundColor: '#ebecf3',
    },
    container: {
        ...margin(16, 16, 0, 16),
        backgroundColor: '#fff',
        borderRadius: 6,
        padding: 8,
    },
    headerContainer: {
        flexDirection: 'row',
        marginBottom: 16,
        alignItems: 'center',
    },
    profilePhoto: {
        width: 48,
        height: 48,
        borderRadius: 24
    },
    infoContainer: {
        flex: 1,
        ...margin(0, 16),
    },
    post: {
        marginLeft: 64,
    },
    image: {
        width: '100%',
        height: 300,
        resizeMode: 'contain',
        borderRadius: 6,
    },
    details: {
        flexDirection: 'row',
        marginTop: 8,
    },
    likes: {
        flexDirection: 'row',
        alignItems: 'center'
    },
    comments: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 16
    }
})
