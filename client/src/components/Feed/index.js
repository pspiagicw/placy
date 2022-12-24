import { FlatList, StyleSheet, Text, View, Image } from 'react-native'
import React from 'react'
import { Entypo, Ionicons } from '@expo/vector-icons'

const Feed = (props) => {
    const renderPost = ({ item }) => (
        <View style={styles.PostContainer}>
            <View style={styles.PostHeaderContainer}>
                <Image style={styles.PostProfilePhoto} source={{ uri: item.user.profilePhotoUrl }} />
                <View style={styles.PostInfoContainer}>
                    <Text style={{ fontSize: 16, margin: 0, padding: 0, color: '#0f0f0f' }}>{item.user.username}</Text>
                    <Text style={{ fontSize: 11, ...margin(4, 0, 0, 0), padding: 0, color: '#c1c3cc' }}>{item.postedAt}</Text>
                </View>
                <View style={styles.PostOptions}>
                    <Entypo name="dots-three-horizontal" size={16} color="#73788b" />
                </View>
            </View>
            <View style={styles.Post}>
                <Text>{item.post}</Text>
                <Image style={styles.PostPhoto} source={{ uri: item.photoUrl }} />
                <View style={styles.PostDetails}>
                    <View style={styles.PostLikes}>
                        <Ionicons name="ios-heart-outline" size={24} color="#73788b" />
                        <Text style={{ fontSize: 11, ...margin(0, 0, 0, 8), padding: 0, color: '#0f0f0f' }}>{item.likes}</Text>
                    </View>
                    <View style={styles.PostComments}>
                        <Ionicons name="ios-chatbox-outline" size={24} color="#73788b" />
                        <Text style={{ fontSize: 11, ...margin(0, 0, 0, 8), padding: 0, color: '#0f0f0f' }}>{item.comments}</Text>
                    </View>
                </View>
            </View>
        </View>
    )

    return (
        <View style={styles.Container}>
            <View>
                <Text style={{ fontSize: 32, textAlign: 'center', margin: 0, padding: 0, color: '#0f0f0f' }}>Feed</Text>
            </View>

            <FlatList data={props.feedData} renderItem={renderPost} keyExtractor={item => item.id.toString()} />

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

const styles = StyleSheet.create({
    Container: {
        flex: 1,
        backgroundColor: '#ebecf3',
        // paddingTop: '64px',
    },
    PostContainer: {
        ...margin(16, 16, 0, 16),
        backgroundColor: '#fff',
        borderRadius: 6,
        padding: 8,
    },
    PostHeaderContainer: {
        flexDirection: 'row',
        marginBottom: 16,
        alignItems: 'center',
    },
    PostProfilePhoto: {
        width: 48,
        height: 48,
        borderRadius: 24
    },
    PostInfoContainer: {
        flex: 1,
        ...margin(0, 16),
    },
    Post: {
        marginLeft: 64,
    },
    PostPhoto: {
        // flex: 1,
        // flexDirection: 'row',
        width: '100%',
        height: 300,
        resizeMode: 'contain',
        // alignSelf: 'stretch',
        // height: undefined,
        borderRadius: 6,
        // resizeMode: 'contain',
    },
    PostDetails: {
        flexDirection: 'row',
        marginTop: 8,
    },
    PostLikes: {
        flexDirection: 'row',
        alignItems: 'center'
    },
    PostComments: {
        flexDirection: 'row',
        alignItems: 'center',
        marginLeft: 16
    }
})
