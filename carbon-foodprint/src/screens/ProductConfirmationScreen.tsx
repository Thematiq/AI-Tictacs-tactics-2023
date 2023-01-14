import { View, Text } from "react-native";
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from "../../App";

type Props = NativeStackScreenProps<RootStackParamList, 'ProductConfirmation'>;

export default function ProductConfirmationScreen({ route }: Props) {
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Text>ProductConfirmation {route.params.barcode}</Text>
      </View>
    );
  }