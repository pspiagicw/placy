import { Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React, { useState } from 'react'
import { AntDesign, Octicons } from '@expo/vector-icons';
import mockDelayedResponse from '../../utils/mockDelayedResponse';

const CommentComponent = ({ comment }) => {

    const { id, text, likes, dislikes, children, postedAt, username, profilePhotoUrl } = comment;

    const [isLiked, setIsLiked] = useState(false)
    const [isDisliked, setIsDisliked] = useState(false)

    const [isChildrenExpanded, setIsChildrenExpanded] = useState(true)

    const like = async () => {
        await mockDelayedResponse(() => { }, 200)
        setIsLiked(true)
        setIsDisliked(false)
    }
    const unlike = async () => {
        await mockDelayedResponse(() => { }, 200)
        setIsLiked(false)
    }
    const dislike = async () => {
        await mockDelayedResponse(() => { }, 200)
        setIsDisliked(true)
        setIsLiked(false)
    }
    const undislike = async () => {
        await mockDelayedResponse(() => { }, 200)
        setIsDisliked(false)
    }


    return (
        <TouchableOpacity activeOpacity={0.6} onPress={() => setIsChildrenExpanded(prev => !prev)} style={{ marginLeft: 10, paddingLeft: 10, paddingTop: 10, borderLeftWidth: 0.5 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', }}>
                <View style={{ marginRight: 10 }}>
                    {
                        /**
                         * @TODO
                         * https://reactnative.dev/docs/image.html#defaultsource
                         * Switch to default source
                         * It is kept conditional here because on Android default source does not work in debug mode
                         * Will remove this once the app is ready to ship to production 
                         */
                    }
                    {profilePhotoUrl ?
                        <Image source={{ uri: profilePhotoUrl }} style={{ height: 25, aspectRatio: 1, borderRadius: 50 }} /> :
                        <Image source={{ uri: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png" }} style={{ height: 25, aspectRatio: 1, borderRadius: 50 }} />
                    }
                </View>
                <Text style={{ marginRight: 10 }}>{username}</Text>
                <Text>{postedAt.toString()}</Text>
            </View>
            <View style={{}}>
                <Text>{text}</Text>
            </View>
            <View style={{ flexDirection: 'row', alignSelf: 'flex-end', alignItems: 'center', justifyContent: 'space-evenly', marginBottom: 20 }}>
                <Octicons name="reply" size={16} color="black" style={{ marginRight: 10 }} />
                <View style={{ flexDirection: 'row', alignItems: 'center', marginRight: 10 }}>
                    <TouchableOpacity onPress={!isLiked ? like : unlike}>
                        {isLiked ?
                            <AntDesign name="like1" size={16} color="black" />
                            :
                            <AntDesign name="like2" size={16} color="black" />
                        }
                    </TouchableOpacity>
                    <Text>{likes}</Text>
                </View>
                <View style={{ flexDirection: 'row', alignItems: 'center', marginRight: 10 }}>
                    <TouchableOpacity onPress={!isDisliked ? dislike : undislike}>
                        <AntDesign name={isDisliked ? "dislike1" : "dislike2"} size={16} color="black" />
                    </TouchableOpacity>
                    <Text>{dislikes}</Text>
                </View>
            </View>
            {isChildrenExpanded && children && children.length > 0 && children.map(child => <CommentComponent comment={child} key={child.id} />)}
            {
                /** 
                 * @TODO If not expanded, we render the first child in a small view 
                 * 
                {!isChildrenExpanded && children && children.length > 0 && <View>
                    <Text></Text>
                </View>}
                */
            }
        </TouchableOpacity>
    )
}

const Comments = ({ comments }) => {
    return <View style={{ flex: 1 }}>
        {comments.map(comment => <CommentComponent comment={comment} key={comment.id} />)}
    </View>

}

export default Comments

const styles = StyleSheet.create({})