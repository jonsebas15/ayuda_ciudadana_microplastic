import { HfInference } from '@huggingface/inference';

const hf = new HfInference("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");

export const AI = async (req, res) => {
  try {
    const { prompt } = req.body;
    const out = await hf.chatCompletion({
      model: "mistralai/Mistral-7B-Instruct-v0.2",
      messages: [{ role: "user", content: `Eres un asistente en una pagina web de detecccion de microplasticos, te dire lo que hay en la pagiana web y solo contestas de acuerdo a esto, los colores que se pueden ingresar 
        son Translucido o blanco, Azul, Amarillo, Verde, Negro, Rojo y tambien se pueden Otros. Estos colores se colocan al darle click en la imagen con los microplasticos (es obligatorio). hay un mapa de google y se debe ingresar las cordenadas para poder enviar el archivo (ojo, puedes decirle que busque en el mapa y al darle click 
        se muestran las coordenadas). ahora responde a la siguiente pregunta en el idioma español: ${prompt}` }],
      max_tokens: 80,
      temperature: 0.1,
      seed: 0,
    });

    // Extraer el contenido del mensaje
    const message = out.choices[0].message.content;

    console.log("Respuesta del modelo:", message);
    res.json({ message });
  } catch (error) {
    console.error("Error al procesar la solicitud:", error);
    res.status(500).json({ error: "Error al procesar la solicitud" });
  }
};
