import { Platform, ScrollView, StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import Feed from '../../components/Feed'
import PostItem from '../../components/Feed/PostItem'
import Comments from '../../components/Feed/Comments'
import colors from '../../theme/colors'

const Post = ({ route, navigation }) => {
    const { id } = route.params || ""
    console.log(id)
    const dummyPostData = {
        id: "1",
        user: {
            username: "John Doe",
            profilePhotoUrl: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        },
        postedAt: "2022-12-20T09:25:00 +05:30",
        post: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        photoUrl: "https://dummyimage.com/16:9x1080/",
        likes: 1234,
        comments: 12,
    }

    const dummyComments = [
        {
            id: 1, text: "Magna consectetur est pariatur minim cupidatat minim officia aute magna elit minim labore dolore.", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", profilePhotoUrl: "https://dummyimage.com/16:9x1080/", children: [
                {
                    id: 1.1, text: "Commodo cillum quis commodo est do irure nulla duis magna consequat nisi esse.", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", children: [
                        { id: 1.11, text: "Ad amet id minim ad id non irure ea. ", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", profilePhotoUrl: "https://dummyimage.com/16:9x1080/", children: [] }
                    ]
                },
                {
                    id: 1.2, text: " Fugiat sit eu sit culpa.N", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", profilePhotoUrl: "https://dummyimage.com/16:9x1080/", children: []
                }
            ],
        },
        {
            id: 2, text: "Id pariatur id deserunt et commodo veniam aliqua eiusmod anim quis aute consectetur laboris irure.", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", profilePhotoUrl: "https://dummyimage.com/16:9x1080/", children: [],
        },
        {
            id: 3, text: "Veniam fugiat aliqua ut qui minim est ad veniam elit incididunt ut exercitation ullamco magna.", likes: 2, dislikes: 3, postedAt: new Date(), username: "Kshitiz1403", profilePhotoUrl: "https://dummyimage.com/16:9x1080/", children: []
        }

    ]

    const [imageZoomStatus, setImageZoomStatus] = useState({ id: undefined, isOpen: false })

    return (
        <SafeAreaView style={{ flex: 1, width: Platform.OS == 'web' ? '50%' : '100%', alignSelf: 'center', }}>
            <ScrollView>
                <PostItem id={dummyPostData.id} user={dummyPostData.user} post={dummyPostData.post} postedAt={dummyPostData.postedAt} comments={dummyPostData.comments} imageZoomStatus={imageZoomStatus} setImageZoomStatus={setImageZoomStatus} likes={dummyPostData.likes} photoUrl={dummyPostData.photoUrl} isShownInDiscover={false} />
                <Comments comments={dummyComments} />
            </ScrollView>
            <TouchableOpacity activeOpacity={0.7} style={{ height: 50, justifyContent: 'center', marginHorizontal: 10, }}>
                <Text style={{ color: colors.tertiary, backgroundColor: colors.secondary, padding: 10, paddingHorizontal: 20, borderRadius: 20 }}>Add a comment</Text>
            </TouchableOpacity>

        </SafeAreaView>
    )
}

export default Post

const styles = StyleSheet.create({})