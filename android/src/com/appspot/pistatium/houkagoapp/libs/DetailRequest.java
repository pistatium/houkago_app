package com.appspot.pistatium.houkagoapp.libs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import lombok.Data;

import net.vvakame.util.jsonpullparser.annotation.JsonKey;
import net.vvakame.util.jsonpullparser.annotation.JsonModel;

import org.json.JSONObject;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.VolleyError;
import com.android.volley.RequestQueue.RequestFilter;
import com.android.volley.Response;
import com.android.volley.Response.ErrorListener;
import com.android.volley.Response.Listener;
import com.appspot.pistatium.houkagoapp.models.APIBase;
import com.appspot.pistatium.houkagoapp.models.APIBaseGen;
import com.appspot.pistatium.houkagoapp.models.AppModel;
import com.appspot.pistatium.houkagoapp.models.DeveloperModel;
import com.appspot.pistatium.utilities.L;

public class DetailRequest extends Request<DeveloperModel> {

	private final Listener<DeveloperModel> mListener;
	private Map<String, String> mParams;

	public DetailRequest(int method, String url, Listener<DeveloperModel> listener,
			ErrorListener errorListener) {
		super(method, url, errorListener);
		mListener = listener;
	}


	public void setParams(Map<String, String> map) {
		mParams = map;
	}

	protected Map<String, String> getParams() {
		return mParams;
	}

	protected Response<DeveloperModel> parseNetworkResponse(NetworkResponse networkResponse) {

		String resp = new String(networkResponse.data);
				
		AppModel app = new AppModel();
		DeveloperModel developer = new DeveloperModel();
		try {
			APIBase api = APIBaseGen.get(resp);
			developer = api.getDeveloper();
			developer.save();
			L.d("developer saved");
			
			app = api.getApp();
			AppModel saved_app = AppModel.getById(app.getApp_id());
			if (saved_app != null) {
				saved_app.update(app);
				L.d("app saved");
			}
		} catch (Exception e) {
			L.d("error","json error", e);
			return Response.error(new VolleyError());
		}
		return Response.success(developer, getCacheEntry());
	}


	@Override
	protected void deliverResponse(DeveloperModel response) {
		mListener.onResponse(response);

	}
}
