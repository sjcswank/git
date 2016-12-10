package org.launchcode.blogz.controllers;

import java.awt.List;

import javax.servlet.http.HttpServletRequest;

import org.launchcode.blogz.models.Post;
import org.launchcode.blogz.models.User;
import org.launchcode.blogz.models.dao.PostDao;
import org.launchcode.blogz.models.dao.UserDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class PostController extends AbstractController {
	
	@Autowired
	private PostDao PostDao;
	
	@Autowired
	private UserDao UserDao;

	@RequestMapping(value = "/blog/newpost", method = RequestMethod.GET)
	public String newPostForm() {
		return "newpost";
	}
	
	@RequestMapping(value = "/blog/newpost", method = RequestMethod.POST)
	public String newPost(HttpServletRequest request, Model model) {
		
		String error = null;
		
		//get params		
		String title = request.getParameter("title");
		String body = request.getParameter("body");
		User author = this.getUserFromSession(request.getSession());
		
		//post has title and body
		if (title == null || title == "" || body == null || body == ""){
			error = "Title and Body are Required";
			model.addAttribute("error", error);
			model.addAttribute("value", title);
			model.addAttribute("body", body);
			return "newpost";
		}
		
		//pass params to Post()
		Post post = new Post(title, body, author);
		
		//save to db
		PostDao.save(post);
		
		return "redirect:/blog/" + author.getUsername() + "/" + post.getUid(); 
	}
	
	@RequestMapping(value = "/blog/{username}/{uid}", method = RequestMethod.GET)
	public String singlePost(@PathVariable String username, @PathVariable int uid, Model model) {
		
		Post post = PostDao.findByUid(uid);
		//pass params to post.html
		model.addAttribute("post", post);
		
		return "post";
	}
	
	@RequestMapping(value = "/blog/{username}", method = RequestMethod.GET)
	public String userPosts(@PathVariable String username, Model model) {

		//find user
		User author = UserDao.findByUsername(username);
		
		//pass posts to blog.html
		model.addAttribute("posts", PostDao.findByAuthor(author));
		
		return "blog";
	}
	
}
