import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import BarcodeScannerScreen from './src/screens/BarcodeScannerScreen';
import BasketRecommendationScreen from './src/screens/BasketRecommendationScreen';
import CurrentBasketScreen from './src/screens/CurrentBasketScreen';
import ProductAnalysisScreen from './src/screens/ProductAnalysisScreen';
import ProductConfirmationScreen from './src/screens/ProductConfirmationScreen';
import { Colors } from './src/style/colors';

export type RootStackParamList = {
  CurrentBasket: undefined;
  BarcodeScanner: undefined;
  ProductAnalysis: undefined;
  ProductConfirmation: {
    barcode: string;
  };
  BasketRecommendation: undefined;
  
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const screenOptions = {
  headerTitle: "Carbon Foodprint", 
  headerBackTitle: "",
  headerStyle: { 
    backgroundColor: Colors.transparent 
  }
};

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="CurrentBasket" screenOptions={screenOptions}>
        <Stack.Screen name="CurrentBasket" component={CurrentBasketScreen} />
        <Stack.Screen name="BarcodeScanner" component={BarcodeScannerScreen} />
        <Stack.Screen name="ProductAnalysis" component={ProductAnalysisScreen} />
        <Stack.Screen name="ProductConfirmation" component={ProductConfirmationScreen} />
        <Stack.Screen name="BasketRecommendation" component={BasketRecommendationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


