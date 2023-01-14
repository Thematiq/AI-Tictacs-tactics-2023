import { View, Text } from "react-native";
import { RootStackParamList } from "../../App";
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

type Props = NativeStackScreenProps<RootStackParamList, 'BasketRecommendation'>;


export default function BasketRecommendationScreen(props: Props) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>BasketRecommendationScreen</Text>
      </View>
    );
  }