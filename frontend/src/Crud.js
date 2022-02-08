import Api from "./Api"


export const getItems = async () => {
    try {
        const response = await Api.get("/");
        return response;
    } catch (error) {
        console.error(error);
    }
};

export const postItem = async (item_name) => {
    try {
        const response = await Api.post(`/${item_name}`);
        return response;
    } catch (error) {
        console.error(error);
    }
};

export const deleteItem = async (item_id) => {
    try {
        const response = await Api.delete(`/${item_id}`);
        return response;
    } catch (error) {
        console.error(error);
    }
};