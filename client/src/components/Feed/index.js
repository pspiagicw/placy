import { FlatList, View, Platform } from 'react-native'
import React, { useState } from 'react'
import Scrollbars from 'react-custom-scrollbars'
import PostItem from './PostItem'

const Feed = ({ feedData }) => {

    const [imageZoomStatus, setImageZoomStatus] = useState({ id: '', isOpen: false })

    const Posts = () =>
        <FlatList
            data={feedData}
            keyExtractor={item => item.id.toString()}
            renderItem={({ item }) => {
                const { id, user, postedAt, post, photoUrl, likes, comments } = item;

                return <PostItem id={id} user={user} postedAt={postedAt} post={post} photoUrl={photoUrl} likes={likes} comments={comments} imageZoomStatus={imageZoomStatus} setImageZoomStatus={setImageZoomStatus} />
            }}
        />

    return (
        <View style={{ flex: 1 }}>
            {Platform.OS == 'web' ?
                <Scrollbars>
                    <Posts />
                </Scrollbars> :
                <Posts />
            }
        </View>
    )
}

export default Feed;
