import { StyleSheet, Text, TouchableOpacity } from "react-native";
import { Colors } from "../style/colors";

interface Props {
  title: string;
  textColor?: string;
  backgroundColor?: string;
  onPress: () => void;
}

const FONT_SIZE = 16;

export default function PrimaryButton({ title, onPress, backgroundColor, textColor }: Props) {
    return (
        <TouchableOpacity onPress={onPress}  style={[styles.button, { backgroundColor: backgroundColor ?? Colors.lightGreen }]}>
          <Text style={{ color: textColor ?? Colors.black, fontSize: FONT_SIZE }}>{title}</Text>
          </TouchableOpacity>
    );
  }

  const styles = StyleSheet.create({
    button: {
      alignItems: 'center',
      justifyContent: 'center',
      paddingHorizontal: 24,
      paddingVertical: 12,
      borderRadius: 24,
    },
  });