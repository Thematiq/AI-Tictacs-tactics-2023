import { Text, View, StyleSheet } from "react-native";
import React, { useEffect, useState } from "react";
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { BarCodeScannedCallback, BarCodeScanner } from 'expo-barcode-scanner';
import { RootStackParamList } from "../../App";

type Props = NativeStackScreenProps<RootStackParamList, 'BarcodeScanner'>;

export default function BarcodeScannerScreen({ navigation }: Props) {
    const [hasPermission, setHasPermission] = useState<boolean>();
    const [scanned, setScanned] = useState(false);

    useEffect(() => {
        const getBarCodeScannerPermissions = async () => {
            const { status } = await BarCodeScanner.requestPermissionsAsync();
            setHasPermission(status === 'granted');
        };
    getBarCodeScannerPermissions();
    }, []);

    const handleBarCodeScanned: BarCodeScannedCallback = ({ data }) => {
        setScanned(true);
        navigation.push('ProductConfirmation', { barcode: data })
    };

    if (hasPermission === null) {
        return <Text>Requesting for camera permission</Text>;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }

    return (
        <View style={styles.container}>
            <BarCodeScanner
                onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
                style={StyleSheet.absoluteFillObject} 
            />
        </View>
    );
  }

  const styles = StyleSheet.create({
    container: {
      alignItems: 'center',
      justifyContent: 'center',
      flex: 1
    },
  });