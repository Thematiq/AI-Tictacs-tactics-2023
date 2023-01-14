import { StyleSheet, Text, TouchableOpacity } from "react-native";
import { Colors } from "../style/colors";

interface Props {
  label: string;
  textColor?: string;
  backgroundColor?: string;
  leftComponent?: JSX.Element;
  rightComponent?: JSX.Element;
  onPress: () => void;
}

const FONT_SIZE = 12;

export default function ListItem({ label, leftComponent, rightComponent, backgroundColor, textColor, onPress }: Props) {
    return null;
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