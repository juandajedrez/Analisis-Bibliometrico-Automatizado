import tensorflow as tf  # type:ignore
from tensorflow.keras import backend as K  # type: ignore
from tensorflow.keras import layers, models  # type: ignore

# Supongamos que ya convertimos cada texto a una secuencia de índices de palabra (preprocesamiento)
# y tenemos un vocabulario y longitud máxima (max_len).

vocab_size = 20000  # por ejemplo
embedding_dim = 128
max_len = 50  # longitud máxima de las oraciones (rellenar/truncar)


def crear_rama_lstm():
    """
    Crea una rama de la red que acepta una secuencia de tamaño max_len y la procesa con Embedding + LSTM.
    Se usará la misma arquitectura con pesos compartidos para los dos textos.
    """
    inp = layers.Input(shape=(max_len,), dtype="int32")
    x = layers.Embedding(vocab_size, embedding_dim, input_length=max_len)(inp)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=False))(x)
    x = layers.Dense(64, activation="relu")(x)
    # Opcional: normalizar
    x = layers.Lambda(lambda t: K.l2_normalize(t, axis=1))(x)
    model = models.Model(inputs=inp, outputs=x)
    return model


def distancia_euclidiana(vects):
    """
    Distancia euclidiana entre dos vectores en la tupla.
    """
    x, y = vects
    return K.sqrt(K.sum(K.square(x - y), axis=1, keepdims=True))


def siamese_model():
    # Crear dos entradas (texto A, texto B)
    input_a = layers.Input(shape=(max_len,), name="input_a")
    input_b = layers.Input(shape=(max_len,), name="input_b")

    # La “rama” compartida
    rama = crear_rama_lstm()

    # Obtener embeddings para cada texto
    emb_a = rama(input_a)
    emb_b = rama(input_b)

    # Calcular distancia
    dist = layers.Lambda(distancia_euclidiana, name="dist")([emb_a, emb_b])

    # Puedes usar una capa final para convertir distancia a puntuación de similitud
    # Por ejemplo, usar una función que escala la distancia a un valor entre 0 y 1:
    output = layers.Dense(1, activation="sigmoid")(dist)

    model = models.Model(inputs=[input_a, input_b], outputs=output)
    return model


# Función de pérdida contrastiva (opcional) — ejemplo simplificado
def loss_contrastiva(y_true, y_pred):
    """
    y_true: 1 si textos similares, 0 si no
    y_pred: distancia predicha o valor entre 0 y 1
    """
    margin = 1.0
    # suponiendo que y_pred es la distancia (o trasformación de distancia),
    # podrías usar:
    return K.mean(
        y_true * K.square(y_pred)
        + (1 - y_true) * K.square(K.maximum(margin - y_pred, 0))
    )


# Entrenamiento del modelo
if __name__ == "__main__":
    model = siamese_model()
    model.compile(optimizer="adam", loss=loss_contrastiva, metrics=["accuracy"])
    model.summary()

    # Supón que tienes datos:
    # X1 = matriz (N, max_len) para texto A
    # X2 = matriz (N, max_len) para texto B
    # Y = vectores de tamaño N con 1 (similares) o 0 (no similares)

    # model.fit([X1, X2], Y, batch_size=32, epochs=10, validation_split=0.1)

    # Después, para inferencia:
    # score = model.predict([x1_test, x2_test])
