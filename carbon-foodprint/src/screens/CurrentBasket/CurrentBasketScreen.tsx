import { View, Text, StyleSheet } from "react-native";

export default function CurrentBasketScreen() {
    return (
      <View style={styles.container}>
        <Text>CurrentBasketScreen</Text>
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