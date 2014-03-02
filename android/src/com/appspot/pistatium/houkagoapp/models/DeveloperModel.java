package com.appspot.pistatium.houkagoapp.models;

import java.sql.Date;
import java.util.List;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import net.vvakame.util.jsonpullparser.annotation.JsonKey;
import net.vvakame.util.jsonpullparser.annotation.JsonModel;

import android.provider.BaseColumns;

import com.activeandroid.Model;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.activeandroid.query.Select;
import com.appspot.pistatium.utilities.L;

@Data
@JsonModel(decamelize = false)
@Table(name = "Developer", id = BaseColumns._ID)
public class DeveloperModel extends Model {

	public DeveloperModel() {
		L.d("create");
	}

	@Column(name = "created_at")
	Date created_at = new Date(System.currentTimeMillis());;
	@JsonKey
	@Column(name = "created_stamp")
	long created_stamp = 0;
	
	@Column(name = "updated_at")
	Date updated_at = new Date(System.currentTimeMillis());
	
	@JsonKey
	@Column(name = "updated_stamp")
	long updated_stamp = 0;
	
	@JsonKey(value = "id")
	@Column(name = "developer_id",unique = true, onUniqueConflict = Column.ConflictAction.REPLACE)
	long developer_id;

	@JsonKey
	@Column(name = "status")
	int status;

	@JsonKey(value="uname")
	@Column(name = "user_name")
	String user_name = "";


	@JsonKey
	@Column(name = "tw_name")
	String tw_name;

	@JsonKey
	@Column(name = "fb_addr")
	String fb_addr;

	@JsonKey
	@Column(name = "profile")
	String profile;

	@JsonKey
	@Column(name = "user_alias")
	String user_alias;

	@JsonKey
	@Column(name = "site_addr")
	String site_addr;

	@Column(name = "is_fav")
	boolean is_fav = false;

	@Column(name = "is_read")
	boolean is_read = false;

	public static List<DeveloperModel> getLatest(int count) {
		List<DeveloperModel> apps = new Select().from(DeveloperModel.class).orderBy("_id").limit(count).execute();
		return apps;
	}
	

	
	public static DeveloperModel getById(long developer_id){
		return new Select().from(DeveloperModel.class)
				.where("developer_id = ?", developer_id).executeSingle();
	}
}
