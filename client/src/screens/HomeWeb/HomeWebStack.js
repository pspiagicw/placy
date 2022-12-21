import { View } from 'react-native';
import LeftSidebar from './LeftSidebar';
import MainFeed from './MainFeed';
import RightSidebar from './RightSidebar';

const HomeWebStack = () => {
   return (
      <View style={{ flex: 1, flexDirection: 'row' }}>
         <View style={{ flex: 0.25, backgroundColor: 'green', padding: 20, paddingLeft: 50, paddingTop: 10 }}>
            <LeftSidebar />
         </View>
         <View
            style={{ flex: 0.5, backgroundColor: 'blue', paddingHorizontal: 20, paddingVertical: 10, paddingTop: 10 }}
         >
            <MainFeed />
         </View>
         <View style={{ flex: 0.25, backgroundColor: 'yellow', padding: 20, paddingRight: 50, paddingTop: 10 }}>
            <RightSidebar />
         </View>
      </View>
   );
};

export default HomeWebStack;
