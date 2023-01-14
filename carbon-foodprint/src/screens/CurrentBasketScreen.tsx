import { View, Text, StyleSheet } from "react-native";
import { RootStackParamList } from "../../App";
import PrimaryButton from "../components/PrimaryButton";
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

type Props = NativeStackScreenProps<RootStackParamList, 'CurrentBasket'>;

export default function CurrentBasketScreen({ navigation }: Props) {
    return (
      <View style={styles.container}>
        <Text>CurrentBasketScreen</Text>
        <PrimaryButton title="Add product" onPress={() => navigation.push('BarcodeScanner')} />
      </View>
    );
  }

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
  });