import { View, Text } from "react-native";
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from "../../App";

type Props = NativeStackScreenProps<RootStackParamList, 'ProductAnalysis'>;

export default function ProductAnalysisScreen(props: Props) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>ProductAnalysisScreen</Text>
      </View>
    );
  }