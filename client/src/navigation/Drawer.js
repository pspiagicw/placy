import { DrawerContentScrollView, DrawerItem } from "@react-navigation/drawer";
import { Text } from "react-native-paper";

const CustomDrawer = (props) => {
    const getMockCommunities = () => {
        const length = 20;
        const communities = [];
        for (let i = 0; i < length; i++)
            communities.push({ name: `Community ${i + 1}`, id: i + 1, action: "" })
        return communities;
    }
    const communities = getMockCommunities();

    return <DrawerContentScrollView {...props}>
        <Text>Your Communities</Text>
        {communities.map(community => <DrawerItem label={community.name} key={community.id} />)}
    </DrawerContentScrollView>
}
export default CustomDrawer;